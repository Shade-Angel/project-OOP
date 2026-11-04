import importlib.util
import sys
from pathlib import Path

POINT = Path(__file__).resolve().parent   
ROOT = POINT.parent 
sys.path.insert(0, str(ROOT))  
sys.path.insert(0, str(ROOT / "seed"))           


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Не удалось загрузить модуль из {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    test_files = sorted(POINT.rglob("test_*.py"))
    if not test_files:
        print("Фа1лы с тестами не найдены")
        return 1

    passed = failed = 0
    for file in test_files:
        print(f"\n{file.relative_to(POINT)}")
        try:
            module = load_module(file)
        except Exception as e:
            print(e)
            failed += 1
            continue

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