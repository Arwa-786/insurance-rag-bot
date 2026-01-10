import { useState } from 'react';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false); // LEVEL 8: Loading state

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    // Add user message immediately
    const userMsg = { role: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      const data = await response.json();
      
      // Add bot response
      setMessages((prev) => [...prev, { role: 'bot', text: data.answer }]);
    } catch (err) {
      console.error("Chat Error:", err);
      setMessages((prev) => [...prev, { role: 'bot', text: "Sorry, I'm having trouble connecting to the insurance database." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto p-6 font-sans">
      <header className="flex items-center gap-3 mb-6 border-b pb-4">
        <span className="text-4xl">🦆</span>
        <div>
          <h1 className="text-2xl font-bold text-blue-900">Knight Insurance Agency</h1>
          <p className="text-sm text-gray-500 font-medium">Always here to help with your claims</p>
        </div>
      </header>

      <div className="flex-1 overflow-y-auto border-2 border-gray-100 p-4 mb-4 bg-white shadow-inner rounded-xl">
        {messages.map((m, i) => (
          <div key={i} className={`mb-4 flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-2xl shadow-sm ${
              m.role === 'user' 
                ? 'bg-blue-600 text-white rounded-br-none' 
                : 'bg-gray-100 text-gray-800 rounded-bl-none border border-gray-200'
            }`}>
              {m.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-gray-100 p-3 rounded-2xl animate-pulse text-gray-400 text-sm">
              Assistant is thinking...
            </div>
          </div>
        )}
      </div>

      <div className="flex gap-2 bg-white p-2 border rounded-full shadow-lg">
        <input 
          className="flex-1 px-4 py-2 outline-none rounded-full"
          placeholder="Ask about claims, deductibles..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button 
          onClick={sendMessage} 
          disabled={isLoading}
          className="bg-blue-700 hover:bg-blue-800 text-white px-6 py-2 rounded-full transition-colors disabled:bg-gray-400"
        >
          {isLoading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;