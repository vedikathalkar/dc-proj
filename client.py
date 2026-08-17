import time

import grpc

import resume_pb2
import resume_pb2_grpc

from lamport_clock import LamportClock


# Lamport Logical Clock
clock = LamportClock()


def run():

    print("Connecting to gRPC Server...")

    channel = grpc.insecure_channel(
        "localhost:50052"
    )

    stub = resume_pb2_grpc.ResumeServiceStub(
        channel
    )

    print("Connected Successfully")

    time.sleep(1)

    # ---------------------------------
    # Candidate Details
    # ---------------------------------

    candidate = "Vedika Thalkar"

    role = "Backend Developer"

    resume_text = (
        "Experienced in Python, Django, "
        "REST API design, and SQL databases."
    )

    print(
        f"\nSending resume for "
        f"{candidate} ({role})..."
    )

    # ---------------------------------
    # Send Event
    # ---------------------------------

    client_time = clock.send_event()

    print(
        "Client Lamport Time:",
        client_time
    )

    # ---------------------------------
    # Send RPC Request
    # ---------------------------------

    response = stub.ScreenResume(

        resume_pb2.ResumeRequest(

            candidate_name=candidate,

            resume_text=resume_text,

            job_role=role,

            lamport_time=client_time
        )
    )

    # ---------------------------------
    # Receive Event
    # ---------------------------------

    updated_client_time = clock.receive_event(
        response.lamport_time
    )

    # ---------------------------------
    # Display Result
    # ---------------------------------

    print("\n--- Screening Result ---")

    print(
        f"Candidate: "
        f"{response.candidate_name}"
    )

    print(
        f"Match Score: "
        f"{response.match_score:.2f}%"
    )

    print(
        f"Status: "
        f"{response.status}"
    )

    print(
        f"Matched Skills: "
        f"{response.matched_skills}"
    )

    print(
        f"Server Lamport Time: "
        f"{response.lamport_time}"
    )

    print(
        f"Updated Client Lamport Time: "
        f"{updated_client_time}"
    )

    print("-------------------------")


if __name__ == "__main__":
    run()