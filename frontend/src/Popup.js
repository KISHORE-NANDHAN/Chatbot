import { useState } from "react";
import Chat from "./Chat";

export default function Popup() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      {/* Floating Logo */}
      <div
        onClick={() => setIsOpen(true)}
        style={{
          position: "fixed",
          bottom: "20px",
          right: "20px",
          width: "60px",
          height: "60px",
          background: "url('your-logo.png') no-repeat center center",
          backgroundSize: "cover",
          borderRadius: "50%",
          cursor: "pointer",
          boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.3)",
        }}
      ></div>

      {/* Popup Overlay */}
      {isOpen && (
        <div
          onClick={() => setIsOpen(false)}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            background: "rgba(0, 0, 0, 0.6)",
            zIndex: 1000,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div
            onClick={(e) => e.stopPropagation()}
            style={{
              width: "80%",
              maxWidth: "800px",
              height: "80%",
              background: "white",
              boxShadow: "0px 4px 15px rgba(0, 0, 0, 0.3)",
              borderRadius: "8px",
              position: "relative",
              display: "flex",
              flexDirection: "column",
            }}
          >
            {/* Close Button */}
            <span
              onClick={() => setIsOpen(false)}
              style={{
                position: "absolute",
                top: "10px",
                right: "15px",
                fontSize: "22px",
                fontWeight: "bold",
                color: "#333",
                cursor: "pointer",
              }}
            >
              ×
            </span>

            {/* Chat Component */}
            <Chat />
          </div>
        </div>
      )}
    </div>
  );
}
