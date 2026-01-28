// server.js
// what do these do?
const path = require("path");
const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");

const app = express();
const PORT = 3000;

// --- middleware ---
app.use(cors()); // allow frontend to talk to backend (even if same origin, it's fine)
app.use(express.json()); // parse JSON bodies
app.use(express.static(path.join(__dirname, "public"))); // serve frontend files

// --- database setup --- 
// make new sqlite3 database for tasks
const db = new sqlite3.Database("./tasks.db");

// create table if not exists
db.serialize(() => {
    db.run(`
        CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          done INTEGER NOT NULL DEFAULT 0,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
          )
        `);
});

// helper to convert DB row -> JS object
function rowToTask(row) {
    return {
        id: row.id,
        title: row.title,
        done: !!row.done, // convert 0/1 -> true/false
        createdAt: row.created_at,
    };
}

// --- routes ---

// simple health check