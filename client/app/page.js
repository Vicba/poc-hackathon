"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
    const handleClick = () => {
        console.log("clicked");
    }

    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <Button onClick={handleClick}>Login</Button>

            <div className="mt-10">
                <Link href="/test-score" className="underline text-gray-400 hover:text-gray-700 underline-offset-4">
                    Test score
                </Link>
            </div>
        </main>
    );
}