"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

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

    const onSubmit = ({ score, lessonId }) => {
        console.log({ score, lessonId });
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
