from factory_lowlevel.source_object_generation import build_source_object_generation_report


if __name__ == "__main__":
    report = build_source_object_generation_report()
    print(f"TASK-SOURCE-OBJ-GEN -> {report['status']} ({report['total_records']} records)")
