import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/auth';
import { sql } from '@/lib/db';

// PATCH /api/runs/[id] - Update run status and notes
export async function PATCH(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const session = await auth();

        if (!session?.user?.email) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const { id } = await params;
        const body = await request.json();
        const { status, notes } = body;

        const userId = session.user.email;

        // Update only if the run belongs to the user
        const result = await sql`
      UPDATE runs
      SET status = ${status},
          notes = ${notes !== undefined ? notes : null},
          updated_at = CURRENT_TIMESTAMP
      WHERE id = ${id} AND user_id = ${userId}
      RETURNING *
    `;

        if (result.rows.length === 0) {
            return NextResponse.json({ error: 'Run not found' }, { status: 404 });
        }

        return NextResponse.json({ success: true });
    } catch (error) {
        console.error('Error updating run:', error);
        return NextResponse.json({ error: 'Failed to update run' }, { status: 500 });
    }
}

// DELETE /api/runs/[id] - Delete a run
export async function DELETE(
    request: NextRequest,
    { params }: { params: Promise<{ id: string }> }
) {
    try {
        const session = await auth();

        if (!session?.user?.email) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
        }

        const { id } = await params;
        const userId = session.user.email;

        // Delete only if the run belongs to the user
        const result = await sql`
      DELETE FROM runs
      WHERE id = ${id} AND user_id = ${userId}
      RETURNING id
    `;

        if (result.rows.length === 0) {
            return NextResponse.json({ error: 'Run not found' }, { status: 404 });
        }

        return NextResponse.json({ success: true });
    } catch (error) {
        console.error('Error deleting run:', error);
        return NextResponse.json({ error: 'Failed to delete run' }, { status: 500 });
    }
}
