import { useState } from "react";
import axios from "axios";

export default function Chatbot() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/query";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post(API_URL, { query });
      setResponse(res.data.response);
    } catch (error) {
      setResponse("Erreur lors de la récupération des données.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white p-4">
      <div className="flex flex-col items-center justify-center h-full">
        <h1 className="text-3xl font-semibold text-center mb-6">Chatbot Historique</h1>
        <form className="w-full" onSubmit={handleSubmit}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Posez une question..."
            className="w-full p-3 border border-gray-700 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
          />
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg transition duration-200"
            disabled={loading}
          >
            {loading ? "Recherche..." : "Envoyer"}
          </button>
        </form>
        {response && (
          <div className="mt-6 p-4 bg-gray-700 shadow-md rounded-lg">
            <h2 className="font-bold text-lg text-gray-200">Réponse :</h2>
            <p className="text-gray-300">{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}
