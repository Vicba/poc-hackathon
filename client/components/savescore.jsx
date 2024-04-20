"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import dah from "../lib/abi.json";
import { AbiItem } from "web3-utils";
import Web3 from 'web3';
import { sendTransaction } from "@/web3/ethereum";
import useStore from "@/hooks/useStore";
import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormDescription,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { toast } from "@/components/ui/use-toast";
import { Label } from "@radix-ui/react-label";

export function SaveScore() {
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors },
    } = useForm({defaultValues: {lessonId:1, score:80}});

    const { address } = useStore();
    const web3 = new Web3(window.ethereum);
    const contract = new web3.eth.Contract(
        dah,
        "0x8a2270531063d97555047acb2f79b86cc0173824"
    );
    const onSubmit = async ({ lessonId, score }) => {
        console.log({ lessonId, score });
        const method = contract.methods.uploadScoreOfLesson(lessonId, score);
        const txHash = await sendTransaction(method, contract, address);
        const scoreFromBlockchain = await contract.methods.getAverageScoreOfAddressOfLesson(address, lessonId).call();
        console.log(parseInt(scoreFromBlockchain))
        // console.log(txHash)
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <div>
                <Label htmlFor="lessonId">Lesson ID</Label>
                {/* include validation with required or other standard HTML validation rules */}
                <Input {...register("lessonId", { required: true })} />
                {/* errors will return when field validation fails  */}
                {errors.lessonId && <span>This field is required</span>}
            </div>
            <div className="mt-4">
                <Label htmlFor="score">Score</Label>
                {/* include validation with required or other standard HTML validation rules */}
                <Input {...register("score", { required: true })} />
                {/* errors will return when field validation fails  */}
                {errors.score && <span>This field is required</span>}
            </div>
            <Button type="submit" className="mt-6">
                Save Score
            </Button>
        </form>
    );
}
