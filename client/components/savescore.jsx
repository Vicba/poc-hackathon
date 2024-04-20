"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import dah from "../lib/abi.json";
import { AbiItem } from "web3-utils";
import Web3 from 'web3';
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
    } = useForm();
    const web3 = new Web3(Web3.givenProvider);
    const contract = new web3.eth.Contract(
        dah,
        "0xDA07165D4f7c84EEEfa7a4Ff439e039B7925d3dF"
    );
    console.log("yeees")
    const onSubmit = async ({ score, lessonId }) => {
        console.log({ score, lessonId });
        await contract.methods.uploadScoreOfLesson(lessonId, score).call();
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
