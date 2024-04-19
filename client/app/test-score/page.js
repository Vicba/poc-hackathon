"use client"

import Link from "next/link"

const { SaveScore } = require("@/components/savescore")

const TestScore = () => {
    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <SaveScore />

            <div className="mt-10">
                <Link href="/" className="underline text-gray-400 hover:text-gray-700 underline-offset-4">
                    Login
                </Link>
            </div>
        </main>
    )
}

export default TestScore