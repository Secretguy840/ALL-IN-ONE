let counter = 0;
const timer = setInterval(() => {
    console.log(`Counter: ${counter}`);
    counter++;
    if (counter > 10) {
        clearInterval(timer);
        console.log('Timer stopped');
    }
}, 1000);