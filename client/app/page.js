"use client";

import { Button } from "@/components/ui/button";

export default function Home() {
    const handleClick = () => {
        console.log("clicked");
    }

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <Button onClick={handleClick}>Login</Button>
        </main>
    );
}