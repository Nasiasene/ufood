import time
from typing import Any, Dict, List

from commands.base_command import Command


class CommandBus:
    def __init__(self):
        self._history: List[Dict[str, Any]] = []

    def dispatch(self, command: Command) -> Any:
        started_at = time.perf_counter()
        try:
            result = command.execute()
            status = 'success'
            return result
        except Exception:
            status = 'error'
            raise
        finally:
            elapsed_ms = round((time.perf_counter() - started_at) * 1000, 3)
            self._history.append(
                {
                    'command': command.__class__.__name__,
                    'status': status,
                    'elapsed_ms': elapsed_ms,
                }
            )

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self._history)
