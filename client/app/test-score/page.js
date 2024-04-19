"use client"

const { SaveScore } = require("@/components/savescore")

const TestScore = () => {
    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-24">
            <SaveScore />
        </main>
    )
}

export default TestScore