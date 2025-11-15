// AG-UI Migration: Types now match Pydantic models exactly for proper schema generation

export interface Section {
    idx: number;
    title: string;
    content: string;
    footer: string;
}

export interface Source {
    url: string;
    title: string;
    score: number;
    // Legacy fields for backward compatibility
    content?: string;
    published_date?: string;
}
export type Sources = Record<string, Source>

export interface Log {
    message: string;
    status: string;
}

export interface ProposalSection {
    title: string;
    description: string;
    approved: boolean;
}

// AG-UI compatible: Direct mapping to backend Proposal model
export interface Proposal {
    sections: Record<string, ProposalSection>;
    remarks: string | null;
    approved: boolean;
}

// Legacy enum for backward compatibility
export enum ProposalSectionName {
    Sections = "sections",
}

export type IProposalItem = Record<string, ProposalSection>

// AG-UI Migration: This interface corresponds exactly to agent/state.py ResearchState
export interface ResearchState {
    title: string;
    proposal: Proposal | null;
    outline: Record<string, Record<string, string>>;
    sections: Section[];
    footnotes: string;
    sources: Sources;
    tool: string;
    logs: Log[];
    messages: { [key: string]: unknown }[];
}

// export type Document = Pick<ResearchState, 'sections' | 'title' | 'intro' | 'outline' | 'conclusion' | 'cited_sources'>

