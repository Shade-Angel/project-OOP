import importlib
import sys
from pathlib import Path

POINT = Path(__file__).resolve().parent
ROOT = POINT.parent
sys.path.insert(0, str(POINT))
sys.path.insert(0, str(ROOT))

def main():
    test_files = sorted(POINT.glob("test_*.py"))
    if not test_files:
        print("Фа1лы с тетами не найдены")
        return 1
    
    passed = failed = 0

    for file in test_files:
        module = importlib.import_module(f"tests.{file.stem}")

        for name in sorted(dir(module)):
            if not name.startswith("test_"):
                continue
            try:
                getattr(module, name)()
                print(f"  ok    {name}")
                passed += 1
            except AssertionError as e:
                print(f"  FAIL  {name}: {e}")
                failed += 1
            except Exception as e:
                print(f"  ERROR {name}: {type(e).__name__}: {e}")
                failed += 1

    print("")
    print(f"Итого: {passed} пройдено, {failed} упало")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())