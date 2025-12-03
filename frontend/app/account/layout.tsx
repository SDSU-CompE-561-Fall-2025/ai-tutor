import Sidebar from "@/components/Sidebar";
import ".././globals.css";

export default function AccountLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 ml-64">{children}</div>
    </div>
  );
}
