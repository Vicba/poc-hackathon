import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
    return twMerge(clsx(inputs))
}

export const formatTime = (time) => {
    return String(time).padStart(2, "0");
}
