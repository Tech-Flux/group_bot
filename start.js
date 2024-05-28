const { exec } = require('child_process');

const command = 'python Bot/main.py';
exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error executing command: ${error.message}`);
    return;
  }
  if (stderr) {
    // Check for specific error messages
    if (stderr.includes("No internet connection")) {
      console.error("Error: No internet connection. Please check your network settings.");
    } else if (stderr.includes("Process stopped")) {
      console.error("Process stopped by user.");
    } else {
      console.error(`Error output: ${stderr}`);
    }
    return;
  }
  console.log(`Output: ${stdout}`);
});
