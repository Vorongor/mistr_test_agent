import json
import os
from mistralai import Mistral

from config import SYSTEM_PROMPT, TOOLS_SCHEMA
from tools import names_to_functions


class VoronAgent:
    def __init__(self, model="mistral-large-latest"):
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
        self.model = model
        self.memory = [{"role": "system", "content": SYSTEM_PROMPT}]

    def _manage_memory(self):
        """Helper method to manage memory."""
        if len(self.memory) > 15:
            system_prompt = self.memory[0]
            recent_history = self.memory[-10:]

            start_index = 0
            for i, msg in enumerate(recent_history):
                role = msg.role if hasattr(msg, 'role') else msg.get('role')
                if role == "user":
                    start_index = i
                    break

            self.memory = [system_prompt] + recent_history[start_index:]

    def answer(self, user_input: str):
        self.memory.append({"role": "user", "content": user_input})
        self._manage_memory()

        response = self.client.chat.complete(
            model=self.model,
            messages=self.memory,
            tools=TOOLS_SCHEMA
        )

        msg = response.choices[0].message
        if msg.tool_calls:
            self.memory.append(msg)
            self._handle_tools(msg.tool_calls)
            final_res = self.client.chat.complete(
                model=self.model,
                messages=self.memory
            )
            res_text = final_res.choices[0].message.content
        else:
            res_text = msg.content

        self.memory.append({"role": "assistant", "content": res_text})
        return res_text

    def _handle_tools(self, tool_calls):
        for call in tool_calls:
            func_name = call.function.name
            try:
                args = json.loads(call.function.arguments)
                print(f"\n[System]: Executing {func_name}...")

                result = names_to_functions[func_name](**args)
            except Exception as e:
                result = f"Error executing function: {str(e)}"
                print(f"[Error]: {result}")
            self.memory.append({
                "role": "tool",
                "name": func_name,
                "content": str(result),
                "tool_call_id": call.id
            })
