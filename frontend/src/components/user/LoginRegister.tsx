import { useState } from "react"
import Login from "./Login"
import Register from "./Register"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

const LoginRegister = () => {
  const [mode, setMode] = useState<"login" | "register">("login")

  return (
    <div className="flex justify-center items-center min-h-screen px-4">
      <Card className="w-full max-w-sm mx-auto p-6 shadow-lg">
        <CardContent>
          {mode === "login" ? (
            <>
              <h2 className="text-2xl font-semibold text-center mb-4">Sign in to your account</h2>
              <Login />
              <p className="text-sm text-muted-foreground mt-4 text-center">
                Don't have an account?{" "}
                <Button
                  className="text-blue-500 underline"
                  onClick={() => setMode("register")}
                >
                  Register
                </Button>
              </p>
            </>
          ) : (
            <>
              <h2 className="text-2xl font-semibold text-center mb-4">Create a new account</h2>
              <Register />
              <p className="text-sm text-muted-foreground mt-4 text-center">
                Already have an account?{" "}
                <Button
                  className="text-blue-500 underline"
                  onClick={() => setMode("login")}
                >
                  Sign in
                </Button>
              </p>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default LoginRegister
