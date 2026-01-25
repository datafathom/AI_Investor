import React from 'react';
import { GitBranch, User, Bot } from 'lucide-react';

const ArgumentTree = ({ transcript }) => {
  if (!transcript || transcript.length === 0) return <div className="p-4 text-center text-gray-500">No arguments yet.</div>;

  return (
    <div className="argument-tree p-4 h-full overflow-y-auto">
      <div className="flex flex-col gap-4">
        {transcript.map((msg, idx) => (
            <div key={idx} className={`relative pl-4 border-l-2 ${
                msg.persona === "The Bull" ? "border-green-500/30" :
                msg.persona === "The Bear" ? "border-red-500/30" :
                msg.persona === "User" ? "border-purple-500/30" :
                "border-blue-500/30"
            }`}>
               {/* Connector Dot */}
               <div className={`absolute -left-[5px] top-0 w-2 h-2 rounded-full ${
                  msg.persona === "The Bull" ? "bg-green-500" :
                  msg.persona === "The Bear" ? "bg-red-500" :
                  msg.persona === "User" ? "bg-purple-500" :
                  "bg-blue-500"
               }`}></div>

               <div className="text-xs text-gray-400 mb-1 flex items-center gap-2">
                  <GitBranch size={12} />
                  {msg.parent_id ? `In reply to ${msg.parent_id}` : 'Root'}
                  <span className="opacity-50">#{msg.id || idx+1}</span>
               </div>
               
               <div className="text-sm text-gray-200 bg-white/5 p-2 rounded border border-white/5">
                 {msg.reasoning && msg.reasoning.length > 50 ? msg.reasoning.substring(0, 50) + "..." : msg.reasoning}
               </div>
            </div>
        ))}
      </div>
    </div>
  );
};

export default ArgumentTree;
