
import React from 'react';
import { Microscope, Activity } from 'lucide-react';

const GlobalScanner = () => {
    return (
        <div className="global-scanner-page glass p-8">
            <div className="header flex items-center gap-4 mb-8">
                <Microscope size={32} className="text-burgundy" />
                <h1 className="text-3xl font-bold">Global Asset Scanner</h1>
            </div>

            <div className="card glass p-6 overflow-hidden">
                <table className="w-full text-left">
                    <thead>
                        <tr className="border-b border-gray-700">
                            <th className="p-4">Symbol</th>
                            <th className="p-4">Price</th>
                            <th className="p-4">Change</th>
                            <th className="p-4">AI Sentiment</th>
                            <th className="p-4">Hype Index</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr className="opacity-30 border-b border-gray-800">
                            <td className="p-4">LOADING...</td>
                            <td className="p-4">---</td>
                            <td className="p-4">---</td>
                            <td className="p-4">Searching Path...</td>
                            <td className="p-4"><Activity size={16} /></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default GlobalScanner;
