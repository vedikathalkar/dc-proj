import time
from concurrent import futures

import grpc

import resume_pb2
import resume_pb2_grpc

from lamport_clock import LamportClock


# Lamport Logical Clock
clock = LamportClock()


# Job requirements
JOB_SKILLS = {
    "Data Scientist": [
        "python",
        "machine learning",
        "sql",
        "statistics"
    ],

    "Backend Developer": [
        "python",
        "django",
        "api",
        "sql",
        "docker"
    ],
}


class ResumeService(resume_pb2_grpc.ResumeServiceServicer):

    def ScreenResume(self, request, context):

        print("\n======================================")
        print("Request received from Client")

        # ---------------------------------
        # Receive Event
        # ---------------------------------

        server_time = clock.receive_event(
            request.lamport_time
        )

        print("Client Lamport Time:", request.lamport_time)
        print("Server Lamport Time:", server_time)

        print(
            f"Candidate: {request.candidate_name} "
            f"| Role: {request.job_role}"
        )

        time.sleep(1)

        # ---------------------------------
        # Extract Skills
        # ---------------------------------

        print("\nExtracting skills from resume...")

        resume_lower = request.resume_text.lower()

        required = JOB_SKILLS.get(
            request.job_role,
            []
        )

        matched = [
            skill
            for skill in required
            if skill in resume_lower
        ]

        time.sleep(1)

        # ---------------------------------
        # Calculate Score
        # ---------------------------------

        print("\nScoring candidate...")

        score = (
            len(matched) / len(required) * 100
        ) if required else 0

        status = (
            "Shortlisted"
            if score >= 50
            else "Rejected"
        )

        time.sleep(1)

        print(
            f"Match Score: {score:.2f}% "
            f"| Status: {status}"
        )

        print(
            "Matched Skills:",
            ", ".join(matched)
        )

        # ---------------------------------
        # Send Event
        # ---------------------------------

        response_time = clock.send_event()

        print(
            "Sending Response to Client..."
        )

        print(
            "Server Lamport Time:",
            response_time
        )

        print("======================================\n")

        # ---------------------------------
        # Return Response
        # ---------------------------------

        return resume_pb2.ResumeResponse(

            candidate_name=request.candidate_name,

            match_score=score,

            status=status,

            matched_skills=", ".join(matched),

            lamport_time=response_time
        )


def serve():

    print(
        "Starting gRPC Resume Screening Server..."
    )

    server = grpc.server(
        futures.ThreadPoolExecutor(
            max_workers=10
        )
    )

    resume_pb2_grpc.add_ResumeServiceServicer_to_server(
        ResumeService(),
        server
    )

    server.add_insecure_port(
        "[::]:50052"
    )

    server.start()

    print(
        "Listening on Port: 50052"
    )

    print(
        "Waiting for Client Requests...\n"
    )

    server.wait_for_termination()


if __name__ == "__main__":
    serve()