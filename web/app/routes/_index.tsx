import type { MetaFunction } from "@remix-run/cloudflare";
import { motion } from "motion/react";
import { useEffect, useState } from "react";
import { SearchBar } from "../components/SearchBar";
import HyperText from "../components/ui/hyper-text";
import { useSearchContext } from "../context/SearchContext";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export default function Index() {
  const [rendered, setRendered] = useState(false);
  const { searchQuery, isSearching } = useSearchContext();

  useEffect(() => {
    setRendered(true);
  }, []);

  if (!rendered) {
    return <></>;
  }

  return (
    <motion.div className="flex h-screen items-center justify-center font-grotesque flex-col -mt-10">
      {isSearching && (
        <div>
          <HyperText
            className="text-4xl font-bold text-black dark:text-white"
            text={`${searchQuery}`}
          />
        </div>
      )}
      {!isSearching && (
        <>
          <motion.div
            className="text-8xl font-black"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.2 }}
          >
            Mango
          </motion.div>

          <motion.h2
            className="text-2xl font-bold text-neutral-500"
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
          >
            Get your rare disease treated now, for free.
          </motion.h2>

          <div className="max-w-xl w-full mt-5">
            <SearchBar />
          </div>
        </>
      )}
    </motion.div>
  );
}
