import React from 'react';
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { AlertTriangle } from 'lucide-react';

const RollbackConfirmModal = ({ isOpen, onClose, onConfirm }) => {
    return (
        <AlertDialog open={isOpen} onOpenChange={onClose}>
            <AlertDialogContent className="bg-gray-950 border-gray-800 text-white">
                <AlertDialogHeader>
                    <div className="flex items-center gap-3 mb-2">
                        <div className="h-10 w-10 bg-red-900/30 rounded-full flex items-center justify-center">
                            <AlertTriangle className="h-6 w-6 text-red-500" />
                        </div>
                        <AlertDialogTitle className="text-xl">Confirm Rollback</AlertDialogTitle>
                    </div>
                    <AlertDialogDescription className="text-gray-400">
                        This will immediately redirect ALL traffic to the previous stable environment. 
                        Active user sessions on the current environment may experience a brief interruption.
                        <br /><br />
                        <span className="text-red-400 font-semibold underline">This action cannot be undone automatically.</span>
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel onClick={onClose} className="bg-transparent border-gray-700 hover:bg-gray-900 text-gray-300">
                        Cancel
                    </AlertDialogCancel>
                    <AlertDialogAction 
                        onClick={onConfirm}
                        className="bg-red-600 hover:bg-red-700 text-white font-bold"
                    >
                        PERFORM ROLLBACK
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    );
};

export default RollbackConfirmModal;
