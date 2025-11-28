import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/auth';
import { sql, getOrCreateUser } from '@/lib/db';
import { Challenge } from '@/data';

export interface Run {
    id: string;
    timestamp: number;
    className: string;
    build: string;
    challenges: Challenge[];
    status: 'active' | 'completed' | 'failed';
    notes?: string;
}

// GET /api/runs - Get all runs for the authenticated user
export async function GET() {
    try {
        const session = await auth();

        if (!session?.user?.email) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const userId = session.user.email;

        const result = await sql`
      SELECT id, timestamp, class_name as "className", build, challenges, status, notes
      FROM runs
      WHERE user_id = ${userId}
      ORDER BY timestamp DESC
    `;

        return NextResponse.json(result.rows);
    } catch (error) {
        console.error('Error fetching runs:', error);
        return NextResponse.json({ error: 'Failed to fetch runs' }, { status: 500 });
    }
}

// POST /api/runs - Create a new run
export async function POST(request: NextRequest) {
    try {
        const session = await auth();

        if (!session?.user?.email) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        // Ensure user exists in database
        await getOrCreateUser(
            session.user.email,
            session.user.name || undefined,
            session.user.image || undefined
        );

        const body = await request.json();
        const { className, build, challenges, status, notes } = body;

        const id = `run_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        const timestamp = Date.now();
        const userId = session.user.email;

        await sql`
      INSERT INTO runs (id, user_id, timestamp, class_name, build, challenges, status, notes)
      VALUES (${id}, ${userId}, ${timestamp}, ${className}, ${build}, ${JSON.stringify(challenges)}, ${status}, ${notes || null})
    `;

        const newRun: Run = {
            id,
            timestamp,
            className,
            build,
            challenges,
            status,
            notes,
        };

        return NextResponse.json(newRun, { status: 201 });
    } catch (error) {
        console.error('Error creating run:', error);
        return NextResponse.json({ error: 'Failed to create run' }, { status: 500 });
    }
}
