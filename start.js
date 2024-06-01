import cfonts from 'cfonts';
import chalk from 'chalk';
import os from 'os';
import fs from 'fs';
import { spawn } from 'child_process';
import http from 'http';
import path from 'path';
import { fileURLToPath } from 'url';
import open from 'open';

const { say } = cfonts;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function startPythonScript() {
    console.log('Halima-Bot Starting...');
    const pythonProcess = spawn('python', ['Bot/main.py']);

    say('Halima-Bot', {
        font: 'chrome',
        align: 'center',
        gradient: ['red', 'magenta']
    });
    say('Team Poison', {
        font: 'console',
        align: 'center',
        gradient: ['cyan', 'magenta']
    });

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

function listFilesWithDelay(folderPath, delay) {
    try {
        const files = fs.readdirSync(folderPath);

        const iterateFiles = (index) => {
            if (index < files.length) {
                const fileName = files[index].replace(/\.py$/, ''); 
                console.log(chalk.greenBright("                Module ") + chalk.yellow(fileName));
                setTimeout(() => iterateFiles(index + 1), delay);
            }
        };

        iterateFiles(0);
    } catch (error) {
        console.error(`Error reading folder: ${error}`);
    }
}

const groups = './Bot/groups';
const privates = './Bot/private';
const delay = 1000;

listFilesWithDelay(groups, delay);
listFilesWithDelay(privates, delay);

startPythonScript();
console.log("                " + chalk.yellow(`🖥️ ${os.type()}, ${os.release()} - ${os.arch()}`));
const ramInGB = os.totalmem() / (1024 * 1024 * 1024);
console.log("                " + chalk.yellow(`💾 Total RAM: ${ramInGB.toFixed(2)} GB`));
const freeRamInGB = os.freemem() / (1024 * 1024 * 1024);
console.log("                " + chalk.yellow(`💽 Free RAM: ${freeRamInGB.toFixed(2)} GB`));
console.log("                " + chalk.yellow(`📃 Script by Abdul`));


const htmlFilePath = path.join(__dirname, 'Halima/main.html');

const server = http.createServer((req, res) => {
    fs.readFile(htmlFilePath, (err, data) => {
        if (err) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.write('404 Not Found');
        } else {
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.write(data);
        }
        res.end();
    });
});

server.listen(8080, () => {
    console.log(chalk.green("Server is running on port 8080"));

    /**uncomment to auto open webpage of the bot in your machine */

   open('http://localhost:8080'); 
});

