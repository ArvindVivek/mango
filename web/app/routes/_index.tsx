import type { MetaFunction } from "@remix-run/cloudflare";
import { AnimatePresence, motion } from "motion/react";
import { useEffect, useState } from "react";
import { SearchBar } from "../components/SearchBar";
import HyperText from "../components/ui/hyper-text";
import { useSearchContext } from "../context/SearchContext";
import { VelocityScroll } from "../components/ui/scroll-based-velocity";
import { TrialCard } from "../components/TrialCard";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

const boxVariant = {
  hidden: {
    scale: 0.5,
    opacity: 0,
  },
  visible: {
    scale: 1,
    opacity: 1,
    transition: {
      when: "beforeChildren", //use this instead of delay
      staggerChildren: 0.1, //apply stagger on the parent tag
    },
  },
};

const listVariant = {
  hidden: {
    x: -10, //move out of the site
    opacity: 0,
  },
  visible: {
    x: 0, // bring it back to nrmal
    opacity: 1,
  },
};

export default function Index() {
  const [rendered, setRendered] = useState(false);
  const { searchQuery, isSearching, results } = useSearchContext();

  useEffect(() => {
    setRendered(true);
  }, []);

  if (!rendered) {
    return <></>;
  }

  return (
    <AnimatePresence>
      <motion.div
        layout
        className="flex h-screen items-center justify-center font-grotesque flex-col overflow-scroll py-10"
      >
        {isSearching && (
          <motion.div layout>
            <div className="">
              <HyperText
                className="text-4xl font-bold "
                text={`${searchQuery}`}
              />
            </div>
            <VelocityScroll
              text="Finding the best treatment for you"
              default_velocity={5}
              className="font-display text-center text-4xl font-bold tracking-[-0.02em] text-black drop-shadow-sm dark:text-white md:text-7xl md:leading-[5rem]"
            />
          </motion.div>
        )}

        {!isSearching && (
          <>
            <motion.div
              className="text-8xl font-black -mt-40"
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

        {results.length >= 0 && (
          <motion.div
            layout
            className="flex flex-col gap-4 w-full max-w-3xl mt-5"
            variants={boxVariant}
            animate="visible"
            initial="hidden"
          >
            {results.map((trial, id) => (
              <motion.li key={id} className="list-none" variants={listVariant}>
                <TrialCard trial={trial} animKey={id} />
              </motion.li>
            ))}
          </motion.div>
        )}
      </motion.div>
    </AnimatePresence>
  );
}
