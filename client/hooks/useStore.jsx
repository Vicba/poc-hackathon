import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

const useStore = create(
  persist(
    (set) => ({
      isLoggedIn: false,
      questions: [],
      currentQuestion: 0,
      score: 0,
      quizId: null,
      totalTime: 0,
      setIsLoggedIn: (isLoggedIn) => set({ isLoggedIn }),
      setQuestions: (questions) => set({ questions }),
      setScore: (score) => set({ score }),
      removeQuestions: () => set({ questions: [] }),
      incrementCurrentQuestion: () =>
        set((state) => ({ currentQuestion: state.currentQuestion + 1 })),
      resetCurrentQuestion: () => set({ currentQuestion: 0 }),
      resetScore: () => set({ score: 0 }),
      resetQuizId: () => set({ quizId: null }),
      setQuizId: (id) => set({ quizId: id }),
      incrementTotalTime: (time) => set({ totalTime: state.totalTime + time }),
      resetTotalTime: () => set({ totalTime: 0 }),
      resetEverything: () => {
        set({ questions: [] });
        set({ currentQuestion: 0 });
        set({ quizId: null });
        set({ totalTime: 0 });
      },
    }),
    {
      name: "sportify-store",
      storage: createJSONStorage(() => localStorage),
    }
  )
);

export default useStore;
