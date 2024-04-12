# pyarithmeticlib

A package to generate arithmetic expression

## Installation

```bash
$ pip install pyarithmeticlib
```

## Usage

`pyarithmeticlib` can be used to generate arithmetic expressions as follows:

```python
from pyarithmeticlib.expression import Addition, Multiplication
from pyarithmeticlib.generator import ExpressionGenerator

generator = ExpressionGenerator(
    max_depth=2, min_length=2, max_length=4, min_value=1,
    max_value=10, min_n_operands=1, max_n_operands=3,
    allowed_operations={Addition, Multiplication}, seed=42
)

for expr in generator.yield_expressions(5):
    print(expr)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`pyarithmeticlib` was created by amaurylekens. It is licensed under the terms of the MIT license.

## Credits

`pyarithmeticlib` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
