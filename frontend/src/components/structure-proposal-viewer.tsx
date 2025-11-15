"use client"

// AG-UI Migration: Updated to work with new Proposal structure from Pydantic models

import { useCallback, useState } from "react"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Proposal, ProposalSection } from "@/lib/types";
import { Textarea } from "@/components/ui/textarea";

function ProposalItem({
    proposal,
    renderSection,
    title,
}: {
    proposal: Proposal
    renderSection: (sectionKey: string, section: ProposalSection) => React.ReactNode
    title: string
}) {
    return (
        <div>
            <h3 className="text-lg font-semibold">{title}</h3>
            {Object.entries(proposal.sections).map(([key, section]) =>
                renderSection(key, section)
            )}
        </div>
    )
}

export function ProposalViewer({
    proposal,
    onSubmit,
}: {
    proposal: Proposal
    onSubmit: (approved: boolean, proposal: Proposal) => void,
}) {
    const [reviewedProposal, setReviewedProposal] = useState(proposal)

    const handleCheckboxChange = (
        sectionKey: string,
        checked: boolean
    ) => {
        setReviewedProposal((prev) => ({
            ...prev,
            sections: {
                ...prev.sections,
                [sectionKey]: {
                    ...prev.sections[sectionKey],
                    approved: checked
                }
            }
        }))
    }

    const handleRemarksChange = (
        remarks: string
    ) => {
        setReviewedProposal((prev) => ({
            ...prev,
            remarks: remarks || null,
        }))
    }

    const handleSubmit = useCallback((approved: boolean) => {
        onSubmit(approved, {...reviewedProposal, approved})
    }, [onSubmit, reviewedProposal])

    const renderSection = (
        sectionKey: string,
        section: ProposalSection
    ) => (
        <div key={sectionKey} className="flex items-start space-x-2 mb-2">
            <Checkbox
                id={sectionKey}
                checked={section.approved}
                onCheckedChange={(checked) => handleCheckboxChange(sectionKey, checked as boolean)}
                className="border border-black/10 data-[state=checked]:text-[var(--primary)]"
            />
            <div className="grid gap-1.5 leading-none">
                <label
                    htmlFor={sectionKey}
                    className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                    {section.title}
                </label>
                <p className="text-sm text-muted-foreground">{section.description}</p>
            </div>
        </div>
    )

    return (
        <Card className="w-full max-w-4xl mx-auto border-black/10 shadow-none rounded-none">
            <CardHeader>
                <CardTitle>Research Paper Proposal</CardTitle>
                <CardDescription>
                    I&apos;ve prepared a proposal for structuring your research. Feel free to modify any sections or points to better match your needs - we can adjust until it&apos;s exactly what you&apos;re looking for.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <ScrollArea className="h-[60vh] pr-4">
                    <div className="space-y-6">
                        {ProposalItem({ title: 'Sections', proposal: reviewedProposal, renderSection })}
                        <div className="space-y-2">
                            <label htmlFor="remarks" className="text-sm font-medium">
                                Additional Remarks
                            </label>
                            <Textarea
                                id="remarks"
                                placeholder="Enter any additional feedback or remarks..."
                                className="min-h-[100px] border-black/10 resize-none"
                                onChange={(e) => handleRemarksChange(e.target.value)}
                                value={reviewedProposal.remarks || ''}
                            />
                        </div>
                    </div>
                </ScrollArea>
            </CardContent>
            <CardFooter className="flex justify-between">
                <Button
                    onClick={() => handleSubmit(false)}
                    className="text-red-500"
                    disabled={!reviewedProposal.remarks?.length}
                >
                    Reject Proposal
                </Button>
                <Button
                    onClick={() => handleSubmit(true)}
                    className="bg-[var(--primary)] text-white hover:bg-[#68330d]"
                    disabled={!Object.values(reviewedProposal.sections).some(section => section.approved)}
                >
                    Approve Proposal
                </Button>
            </CardFooter>
        </Card>
    )
}
