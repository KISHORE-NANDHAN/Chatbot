import { useState, useEffect } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000"); // Connect to backend

export default function Chat() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  useEffect(() => {
    // Listen for chatbot responses
    socket.on("botResponse", (data) => {
      setChat((prevChat) => [...prevChat, { text: data.response, sender: "bot" }]);
    });

    return () => socket.off("botResponse"); // Cleanup on unmount
  }, []);

  const sendMessage = () => {
    if (message.trim() !== "") {
      setChat((prevChat) => [...prevChat, { text: message, sender: "user" }]);
      socket.emit("chatMessage", message); // Send message to backend
      setMessage("");
    }
  };

  return (
    <div className="flex flex-col w-full h-full p-6 bg-gray-100 rounded-lg shadow-lg max-w-3xl mx-auto">
      <h2 className="text-xl font-semibold text-gray-800 text-center mb-4">College Chatbot</h2>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto bg-white border border-gray-300 rounded-lg p-4 shadow-sm max-h-96">
        {chat.map((msg, index) => (
          <div key={index} className={`mb-3 flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`px-4 py-2 rounded-lg shadow-md ${
                msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"
              }`}
            >
              <strong>{msg.sender === "user" ? "You: " : "Bot: "}</strong> {msg.text}
            </div>
          </div>
        ))}
      </div>

      {/* Message Input */}
      <div className="flex items-center mt-4">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 outline-none"
        />
        <button
          onClick={sendMessage}
          className="ml-3 px-5 py-3 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition duration-300"
        >
          Send
        </button>
      </div>
    </div>
  );
}
