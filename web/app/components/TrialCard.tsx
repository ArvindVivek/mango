import { AnimatePresence, motion } from "framer-motion"
import { useState } from "react"
import { Map, Microscope, PlayCircle, Users } from "lucide-react"
import { ClinicalTrial } from "../types/trial"
import mockData from "../mockData/trial.json"
import { cn } from "../lib/utils"

export const TrialCard = ({
    trial = mockData[0],
    animKey,
}: {
    trial: ClinicalTrial | undefined
    animKey: number
}) => {
    const [hovered, setHovered] = useState(false)
    const [expanded, setExpanded] = useState(false)
    return (
        <motion.div
            className="rounded-xl w-full p-2 border-black border-2 font-sans hover:cursor-pointer"
            onHoverStart={() => setHovered(true)}
            onHoverEnd={() => setHovered(false)}
            animate={{ scale: hovered ? 1.01 : 1 }}
            onClick={() => setExpanded(!expanded)}
        >
            {/* heading */}
            <div className="flex flex-row w-full justify-between">
                <div className="font-bold text-2xl">
                    {trial.protocolSection.identificationModule.briefTitle}
                </div>

                <div className="flex flex-row text-sm justify-center items-center gap-1">
                    <Users size={20} />
                    <span className="text-lg">
                        {
                            trial.protocolSection.designModule.enrollmentInfo
                                .count
                        }
                    </span>
                </div>
            </div>
            {/* sub title  */}
            <div className="text-neutral-500 mb-2">
                {trial.protocolSection.identificationModule.officialTitle}
            </div>

            {/* Recruiting status */}
            <div className="flex flex-row items-center gap-2">
                <span className="relative flex h-3 w-3">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                </span>
                <span className="text-sm">Accepting participants</span>
            </div>

            {/* Sponsoring institution  */}
            <div className="flex text-sm flex-row items-center gap-1">
                <Microscope size={16} />
                {
                    trial.protocolSection.sponsorCollaboratorsModule.leadSponsor
                        .name
                }{" "}
            </div>
            {/* location */}
            <div className="flex text-sm flex-row items-center gap-1">
                <Map size={16} />
                {trial.protocolSection.contactsLocationsModule?.locations?.map(
                    (location, id) => (
                        <Location key={id} location={location} />
                    )
                )}
            </div>
            {/* Expected start date */}
            <div className="flex text-sm flex-row items-center gap-1">
                <PlayCircle size={16} />
                {trial.protocolSection.statusModule.startDateStruct.date}
            </div>

            {/* tags */}
            <div className={cn("flex mt-2 gap-1", expanded ? "mb-10" : "")}>
                {trial.protocolSection.conditionsModule.conditions.map(
                    (condition: string, id) => (
                        <ConditionTag key={id} condition={condition} />
                    )
                )}
            </div>

            <AnimatePresence key={`expanded-trial-card-${animKey}`}>
                {expanded && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{
                            opacity: 1,
                            height: "auto",
                            transition: {
                                duration: 0.2,
                            },
                        }}
                        exit={{
                            opacity: 0,
                            height: 0,
                            transition: {
                                duration: 0.1,
                            },
                        }}
                        className="overflow-hidden"
                    >
                        <div className="text-xl font-bold ">Summary</div>
                        <div className="text-sm">
                            {
                                trial.protocolSection.descriptionModule
                                    .briefSummary
                            }
                        </div>

                        <div className="text-xl font-bold mt-10">Contact</div>
                        <div className="text-sm">
                            {trial.protocolSection.contactsLocationsModule?.centralContacts?.map(
                                (contact, id) => (
                                    <div
                                        key={id}
                                        className="flex flex-col mt-1"
                                    >
                                        <div className="font-bold">
                                            {contact.name}
                                        </div>
                                        <div className="text-sm">
                                            {contact.phone}
                                        </div>
                                        <div className="text-sm">
                                            {contact.email}
                                        </div>
                                    </div>
                                )
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    )
}

export const Location = ({ location }: { location: ClinicalTrialLocation }) => {
    return (
        <div className="text-black flex flex-row text-center justify-center items-center rounded-full">
            {location.city}, {location.state}
        </div>
    )
}

interface ClinicalTrialLocation {
    facility: string
    status: string
    city: string
    state: string
    zip: string
    country: string
    contacts: {
        name: string
        role: string
        phone: string
    }[]
    geoPoint: {
        lat: number
        lon: number
    }
}
export const ConditionTag = ({ condition }: { condition: string }) => {
    return (
        <div className="bg-neutral-200 text-black flex flex-row text-center justify-center items-center rounded-full px-2 py-1 text-xs">
            {condition}
        </div>
    )
}
