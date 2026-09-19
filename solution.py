import json
import pennylane as qp
import pennylane.numpy as np
dev = qp.device("default.qubit", wires=3)

@qp.qnode(dev)
def model(alpha):
    """In this qnode you will define your model in such a way that there is a single 
    parameter alpha which returns each of the basic states.

    Args:
        alpha (float): The only parameter of the model.

    Returns:
        (numpy.tensor): The probability vector of the resulting quantum state.
    """

    # Put your code here #
    # Wire 2 (least-significant bit): one full flip per unit of alpha.
    qp.RX(np.pi * alpha, wires=2)

    # Wire 1: half the frequency, then remove the LSB's share of the angle.
    qp.RX(np.pi * alpha / 2, wires=1)
    qp.CRX(-np.pi / 2, wires=[2, 1])

    # Wire 0 (most-significant bit): quarter frequency, then remove the two lower bits' shares.
    qp.RX(np.pi * alpha / 4, wires=0)
    qp.CRX(-np.pi / 4, wires=[2, 0])
    qp.CRX(-np.pi / 2, wires=[1, 0])

    return qp.probs(wires=[0, 1, 2])

def generate_coefficients():
    """This function must return a list of 8 different values of the parameter that
    generate the states 000, 001, 010, ..., 111, respectively, with your ansatz.

    Returns:
        (list(int)): A list of eight real numbers.
    """
    

    return [0, 1, 2, 3, 4, 5, 6, 7]
# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    return None

def check(solution_output, expected_output: str) -> None:
    coefs = generate_coefficients()
    output = np.array([model(c) for c in coefs])
    epsilon = 0.001

    for i in range(len(coefs)):
        assert np.isclose(output[i][i], 1)

    def is_continuous(function, point):
        limit = calculate_limit(function, point)

        if limit is not None and sum(abs(limit - function(point))) < epsilon:
            return True
        else:
            return False

    def is_continuous_in_interval(function, interval):
        for point in interval:
            if not is_continuous(function, point):
                return False
        return True

    def calculate_limit(function, point):
        x_values = [point - epsilon, point, point + epsilon]
        y_values = [function(x) for x in x_values]
        average = sum(y_values) / len(y_values)

        return average

    assert is_continuous_in_interval(model, np.arange(0,10,0.001))

    for coef in coefs:
        assert coef >= 0 and coef <= 10

# These are the public test cases
test_cases = [
    ('No input', 'No output')
]
# This will run the public test cases locally
for i, (input_, expected_output) in enumerate(test_cases):
    print(f"Running test case {i} with input '{input_}'...")

    try:
        output = run(input_)

    except Exception as exc:
        print(f"Runtime Error. {exc}")

    else:
        if message := check(output, expected_output):
            print(f"Wrong Answer. Have: '{output}'. Want: '{expected_output}'.")

        else:
            print("Correct!")
