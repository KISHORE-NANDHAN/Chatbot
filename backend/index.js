const express = require("express");
const app = express();
const mongoose = require("mongoose");
const http = require("http"); 
const { Server } = require("socket.io");
const env = require('dotenv').config();

const server = http.createServer(app); // Corrected this line
const io = new Server(server, { cors: { origin: "*" } }); 
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

console.log("MONGO_URI Loaded:", process.env.MONGO_URI);

// Connect to MongoDB
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
}).catch(
  (err) => console.log(err)
).then(
  () => console.log("MongoDB Connected...")
);

// WebSocket Connection
io.on("connection", (socket) => {
  console.log("User connected:", socket.id);

  socket.on("chatMessage", async (message) => {
    console.log("User message:", message);

    const collegeInfo = await fetchCollegeInfo(message);
    socket.emit("botResponse", { response: collegeInfo || "I don't know that yet!" });
  });

  socket.on("disconnect", () => {
    console.log("User disconnected:", socket.id);
  });
});

// REST API for fetching data from MongoDB
app.get("/college-info/:query", async (req, res) => {
  const query = req.params.query;
  const data = await fetchCollegeInfo(query);
  res.json({ response: data || "No information found!" });
});

const fetchCollegeInfo = async (query) => {
  return "Example College Info Response";
};

server.listen(5000, () => {
  console.log("Server running on port 5000");
});
