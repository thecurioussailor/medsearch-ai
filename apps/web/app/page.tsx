import { Disclaimer } from "@/components/Disclaimer";
import { Header } from "@/components/Header";
import { SearchWorkspace } from "@/components/SearchWorkspace";
import { WelcomeSection } from "@/components/WelcomeSection";

export default function Home() {
  return (
    <>
      <Header />
      <main className="flex flex-1 flex-col">
        <div className="mx-auto flex w-full min-w-0 max-w-3xl flex-1 flex-col gap-8 px-4 pt-10 pb-8 sm:px-6 sm:pt-14 lg:pt-16">
          <WelcomeSection />
          <SearchWorkspace />
          <div className="mt-auto pt-2">
            <Disclaimer />
          </div>
        </div>
      </main>
    </>
  );
}
