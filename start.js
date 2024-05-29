import cfonts from 'cfonts';
import chalk from 'chalk';
const { say } = cfonts;
import os from 'os';
import { spawn } from 'child_process';
function startPythonScript() {
    console.log('Halima-Bot Starting...');
    const pythonProcess = spawn('python', ['Bot/main.py']);

    say('Halima-Bot', {
        font: 'chrome',
        align: 'center',
        gradient: ['red', 'magenta']
      })
      say(`Team Poison`, {
        font: 'console',
        align: 'center',
        gradient: ['cyan', 'magenta']
      })
      

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Python stdout: ${data}`);
    });


    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python stderr: ${data}`);
    });

    pythonProcess.on('exit', (code) => {
        console.log(`Python script exited with code ${code}. Restarting...`);
        startPythonScript();
    });

}

startPythonScript();
console.log(chalk.yellow(`🖥️ ${os.type()}, ${os.release()} - ${os.arch()}`));
const ramInGB = os.totalmem() / (1024 * 1024 * 1024);
console.log(chalk.yellow(`💾 Total RAM: ${ramInGB.toFixed(2)} GB`));
const freeRamInGB = os.freemem() / (1024 * 1024 * 1024);
console.log(chalk.yellow(`💽 Free RAM: ${freeRamInGB.toFixed(2)} GB`));
console.log(chalk.yellow(`📃 Script by Abdul`));




