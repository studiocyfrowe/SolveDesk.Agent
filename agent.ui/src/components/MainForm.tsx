import { faPlay } from "@fortawesome/free-solid-svg-icons"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome"
import React from "react"
import { useForm } from "react-hook-form"

interface FormValues {
    query: string
}

interface MainFormProps {
    runAgent: (query: string) => void // 🔥 FIX
    loading: boolean
}

const MainForm: React.FC<MainFormProps> = ({ runAgent, loading }) => {
    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isValid }
    } = useForm<FormValues>({
        mode: "onChange" // 🔥 walidacja na żywo
    })

    const onSubmit = (data: FormValues) => {
        const query = data.query.trim()
        runAgent(query)
        reset() // 🔥 czyści input
    }

    return (
        <form
            onSubmit={handleSubmit(onSubmit)}
            className="flex flex-col space-y-2"
        >
            <div className="flex flex-row space-x-3">
                <input
                    type="text"
                    className="border rounded-lg px-3 py-2 w-full"
                    placeholder="Enter command..."
                    {...register("query", {
                        required: "Pole jest wymagane",
                        minLength: {
                            value: 3,
                            message: "Minimum 3 znaki"
                        },
                        validate: value =>
                            value.trim().length > 0 || "Nie może być samą spacją" // 🔥 edge case
                    })}
                />

                <button
                    type="submit"
                    disabled={loading || !isValid} // 🔥 lepsza kontrola
                    className="bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded-lg text-sm flex items-center gap-2 disabled:opacity-50"
                >
                    <FontAwesomeIcon icon={faPlay} />
                    {loading ? "Running..." : "Start"}
                </button>
            </div>

            {errors.query && (
                <span className="text-red-500 text-sm">
                    {errors.query.message}
                </span>
            )}
        </form>
    )
}

export default MainForm