import { useState } from "react"
import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { Menu, X } from "lucide-react"
import { useAuth } from "@/lib/authContext"


const Navbar = () => {
    const { user, logout } = useAuth()
    const [isOpen, setIsOpen] = useState(false)

    const toggleMenu = () => setIsOpen(!isOpen)
    const closeMenu = () => setIsOpen(false)

    return (

        <header className="bg-background border-b border-border shadow-sm">
            <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
                <Link to="/" className="text-xl font-bold" onClick={closeMenu}>
                    Pawgress
                </Link>

                {/* Desktop nav */}
                <nav className="hidden md:flex items-center gap-4">
                    {user ? (
                        <>
                            <Link to="/me" className="text-sm hover:underline">
                                Dashboard
                            </Link>
                            {(user.role === "admin" || user.role === "superuser") && (
                                <Link to="/admin" className="text-sm hover:underline">
                                    Admin
                                </Link>
                            )}
                            {user?.role !== "user" && (
                                <Link
                                    to="/admin/metrics"
                                    className="text-muted-foreground hover:text-white transition"
                                >
                                    📈 Metrics
                                </Link>
                            )}
                            <Button variant="destructive" size="sm" onClick={logout}>
                                Log out
                            </Button>
                        </>
                    ) : (
                        <>
                            <Link to="/" className="text-sm hover:underline">
                                Login
                            </Link>
                            <Link to="/" className="text-sm hover:underline">
                                Sign Up
                            </Link>
                        </>
                    )}
                </nav>

                {/* Mobile toggle */}
                <button
                    className="md:hidden text-foreground"
                    onClick={toggleMenu}
                    aria-label="Toggle menu"
                >
                    {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                </button>
            </div>

            {/* Mobile dropdown */}
            {isOpen && (
                <div className="md:hidden px-4 pb-4 space-y-2">
                    {user ? (
                        <>
                            <Link to="/me" onClick={closeMenu} className="block text-sm hover:underline">
                                Dashboard
                            </Link>
                            {(user.role === "admin" || user.role === "superuser") && (
                                <Link to="/admin" onClick={closeMenu} className="block text-sm hover:underline">
                                    Admin
                                </Link>
                            )}

                            {user?.role !== "user" && (
                                <Link
                                    to="/admin/metrics"
                                    className="text-muted-foreground hover:text-white transition"
                                >
                                    📈 Metrics
                                </Link>
                            )}

                            <Button
                                variant="destructive"
                                size="sm"
                                className="w-full"
                                onClick={() => {
                                    logout()
                                    closeMenu()
                                }}
                            >
                                Log out
                            </Button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" onClick={closeMenu} className="block text-sm hover:underline">
                                Login
                            </Link>
                            <Link to="/register" onClick={closeMenu} className="block text-sm hover:underline">
                                Sign Up
                            </Link>
                        </>
                    )}
                </div>
            )}
        </header>
    )
}

export default Navbar
