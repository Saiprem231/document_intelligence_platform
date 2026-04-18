import { useState, useEffect, useRef } from 'react';
import { BrowserRouter, Routes, Route, Link, useParams, useLocation } from 'react-router-dom';
import axios from 'axios';

// --- COMPONENT: Animated Navbar ---
function Navbar() {
  const location = useLocation();
  
  return (
    <nav className="bg-gradient-to-r from-slate-900 via-indigo-900 to-slate-900 p-4 shadow-2xl sticky top-0 z-50 border-b border-indigo-500/30">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="bg-indigo-500 p-2 rounded-lg transform group-hover:rotate-12 transition-transform duration-300 shadow-lg shadow-indigo-500/50">
            📚
          </div>
          <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white to-indigo-200 tracking-tight">
            DocIntel
          </h1>
        </Link>
        <div className="space-x-2">
          <Link to="/" className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 ${location.pathname === '/' ? 'bg-indigo-500/20 text-white border border-indigo-400/50' : 'text-indigo-200 hover:text-white hover:bg-white/5'}`}>
            Dashboard
          </Link>
          <Link to="/qa" className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 shadow-lg ${location.pathname === '/qa' ? 'bg-indigo-500 text-white shadow-indigo-500/40' : 'bg-white/10 text-white hover:bg-white/20'}`}>
            ✨ AI Assistant
          </Link>
        </div>
      </div>
    </nav>
  );
}

// --- COMPONENT: Dashboard (Grid & Cards) ---
function Dashboard() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/books/')
      .then(res => setBooks(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="max-w-7xl mx-auto p-6 lg:p-12 animate-fade-in-up">
      <div className="mb-12 text-center">
        <h2 className="text-4xl lg:text-5xl font-black text-slate-800 mb-4 tracking-tight">Your Intelligent Library</h2>
        <p className="text-lg text-slate-500 max-w-2xl mx-auto">Select a book to view extracted insights or head over to the AI Assistant to query the entire database at once.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
        {books.map((book, index) => (
          <div 
            key={book.id} 
            className="group bg-white rounded-2xl p-6 shadow-sm hover:shadow-2xl border border-slate-100 hover:border-indigo-100 transition-all duration-300 transform hover:-translate-y-2 flex flex-col justify-between"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div>
              <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform duration-300">
                📖
              </div>
              <h3 className="text-xl font-bold text-slate-800 mb-2 leading-tight">{book.title}</h3>
              <p className="text-sm text-slate-500 mb-4 font-medium flex items-center gap-2">
                <span className="w-4 h-px bg-slate-300"></span> 
                {book.author === 'Unknown Author' ? 'Author Unlisted' : book.author}
              </p>
            </div>
            <Link to={`/book/${book.id}`} className="mt-6 w-full text-center bg-slate-50 text-indigo-600 font-bold py-3 rounded-xl group-hover:bg-indigo-600 group-hover:text-white transition-colors duration-300">
              Explore Insights →
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
}

// --- COMPONENT: Book Detail Page ---
function BookDetail() {
  const { id } = useParams();
  const [book, setBook] = useState(null);

  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/api/books/${id}/`)
      .then(res => setBook(res.data))
      .catch(err => console.error(err));
  }, [id]);

  if (!book) return (
    <div className="flex justify-center items-center h-[60vh]">
      <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-indigo-600"></div>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto p-6 mt-10">
      <Link to="/" className="inline-flex items-center text-slate-500 hover:text-indigo-600 font-semibold mb-8 transition-colors">
        ← Back to Library
      </Link>
      <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
        <div className="bg-gradient-to-r from-indigo-50 to-white p-8 md:p-12 border-b border-slate-100">
          <span className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-bold uppercase tracking-wider mb-4 inline-block">Document Metadata</span>
          <h2 className="text-4xl font-black text-slate-900 mb-4 leading-tight">{book.title}</h2>
          <h4 className="text-xl text-slate-600 font-medium">By {book.author}</h4>
        </div>
        <div className="p-8 md:p-12">
          <h5 className="font-bold text-slate-800 text-lg mb-4 flex items-center gap-2">
            📝 Extracted Summary
          </h5>
          <p className="text-slate-600 leading-relaxed text-lg bg-slate-50 p-6 rounded-2xl border border-slate-100">
            {book.description || "No description available in the database."}
          </p>
          <div className="mt-10">
            <a href={book.book_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 bg-slate-900 text-white px-8 py-4 rounded-xl font-bold hover:bg-indigo-600 transition-colors duration-300 shadow-lg hover:shadow-indigo-500/30">
              Access Original Source 🔗
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

// --- COMPONENT: AI Q&A Interface ---
function QAInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => { scrollToBottom(); }, [messages, isLoading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    
    // Capture history BEFORE adding the new message
    const historyForBackend = messages.map(msg => ({
      role: msg.role === 'ai' ? 'assistant' : 'user',
      content: msg.content
    }));

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/ask/', { 
        question: userMessage.content,
        history: historyForBackend
      });
      const aiMessage = { role: 'ai', content: response.data.answer, source: response.data.source };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'ai', content: 'Connection error. Is the Django server running?' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-4 md:p-6 h-[calc(100vh-80px)] flex flex-col">
      <div className="bg-white flex-1 rounded-3xl shadow-2xl overflow-hidden border border-slate-200 flex flex-col">
        
        {/* Chat Header */}
        <div className="bg-slate-50 p-6 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-slate-800">DocIntel Assistant</h2>
            <p className="text-sm text-slate-500">Powered by RAG & Groq Llama 3.1</p>
          </div>
          <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            System Online
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 p-6 overflow-y-auto bg-slate-50/50">
          {messages.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center px-4 animate-fade-in-up">
              <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center text-4xl mb-6 shadow-inner">
                🤖
              </div>
              <h3 className="text-2xl font-bold text-slate-700 mb-2">How can I help you?</h3>
              <p className="text-slate-500 max-w-md">Ask me for plot summaries, genre classifications, or book recommendations based on our database.</p>
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <div key={idx} className={`mb-6 flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex gap-4 max-w-[85%] md:max-w-[70%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                
                {/* Avatar */}
                <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 shadow-md ${msg.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-white border border-slate-200 text-xl'}`}>
                  {msg.role === 'user' ? '👤' : '🤖'}
                </div>

                {/* Bubble */}
                <div className={`p-5 rounded-2xl shadow-sm ${msg.role === 'user' ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-white text-slate-700 rounded-tl-none border border-slate-100'}`}>
                  <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                  
                  {/* Source Citation */}
                  {msg.source && msg.source !== 'None' && (
                    <div className="mt-4 pt-3 border-t border-slate-100/10">
                      <span className="inline-flex items-center gap-1 text-xs font-bold px-2 py-1 rounded bg-slate-100 text-slate-500">
                        📄 Source: {msg.source}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start mb-6">
              <div className="flex gap-4 max-w-[85%]">
                <div className="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-xl shadow-md">🤖</div>
                <div className="p-5 rounded-2xl rounded-tl-none bg-white border border-slate-100 shadow-sm flex items-center gap-2">
                  <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"></span>
                  <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                  <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-white border-t border-slate-200">
          <form onSubmit={handleSend} className="relative flex items-center">
            <input 
              type="text" 
              value={input} 
              onChange={(e) => setInput(e.target.value)} 
              placeholder="Query the database..." 
              disabled={isLoading} 
              className="w-full bg-slate-50 border border-slate-200 text-slate-800 placeholder-slate-400 rounded-full py-4 pl-6 pr-32 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all shadow-inner disabled:opacity-50" 
            />
            <button 
              type="submit" 
              disabled={isLoading || !input.trim()} 
              className="absolute right-2 top-2 bottom-2 bg-indigo-600 text-white px-6 rounded-full font-bold hover:bg-indigo-700 disabled:bg-slate-300 disabled:text-slate-500 transition-colors shadow-md flex items-center gap-2"
            >
              Send <span>📤</span>
            </button>
          </form>
        </div>

      </div>
    </div>
  );
}

// --- MAIN APP ROUTER ---
export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-100 font-sans selection:bg-indigo-200 selection:text-indigo-900">
        <Navbar />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/book/:id" element={<BookDetail />} />
          <Route path="/qa" element={<QAInterface />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}