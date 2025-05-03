// Image classifier with convolutional layers
async function run() {
  const model = tf.sequential();
  
  // Convolutional layer
  model.add(tf.layers.conv2d({
    inputShape: [28, 28, 1],
    filters: 32,
    kernelSize: 3,
    activation: 'relu'
  }));
  
  // Classification layer
  model.add(tf.layers.dense({
    units: 10,
    activation: 'softmax'
  }));

  // Compile model
  model.compile({
    optimizer: 'adam',
    loss: 'categoricalCrossentropy',
    metrics: ['accuracy']
  });

  // Load MNIST data
  const data = await tf.data.csv('mnist.csv');
  const dataset = data.map(({xs, ys}) => {
    return {xs: Object.values(xs), ys: Object.values(ys)};
  }).batch(32);

  // Train model
  await model.fitDataset(dataset, {
    epochs: 10,
    callbacks: {
      onEpochEnd: (epoch, logs) => {
        console.log(`Epoch ${epoch}: loss = ${logs.loss}`);
      }
    }
  });
}