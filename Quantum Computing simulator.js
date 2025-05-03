// Quantum circuit simulator
class Qubit {
  constructor() {
    this.state = [new Complex(1, 0), new Complex(0, 0)]; // |0⟩ state
  }

  applyGate(matrix) {
    this.state = [
      matrix[0][0].mul(this.state[0]).add(matrix[0][1].mul(this.state[1])),
      matrix[1][0].mul(this.state[0]).add(matrix[1][1].mul(this.state[1]))
    ];
  }

  measure() {
    const prob0 = this.state[0].abs2();
    return Math.random() < prob0 ? 0 : 1;
  }
}

function createEntanglement(q1, q2) {
  // Hadamard gate on first qubit
  const H = [
    [new Complex(1/Math.sqrt(2), 0), new Complex(1/Math.sqrt(2), 0)],
    [new Complex(1/Math.sqrt(2), 0), new Complex(-1/Math.sqrt(2), 0)]
  ];
  q1.applyGate(H);
  
  // CNOT gate
  if (q1.measure() === 1) {
    q2.applyGate([
      [new Complex(0, 0), new Complex(1, 0)],
      [new Complex(1, 0), new Complex(0, 0)]
    ]);
  }
}

// Example usage
const alice = new Qubit();
const bob = new Qubit();
createEntanglement(alice, bob);