const { exec } = require('child_process');

const command = 'python Bot/main.py';
exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error executing command: ${error}`);
    return;
  }
  if (stderr) {
    console.error(`Error output: ${stderr}`);
    return;
  }
  console.log(`Output: ${stdout}`);
});
