import unittest

from pipeline_check import summarize, validate_events


SAMPLE = [
    {"event_id": "api-001", "source": "billing-api", "event_type": "request.completed", "occurred_at": "2026-10-21T09:00:00Z", "payload": {"status": 200, "latency_ms": 181}},
    {"event_id": "api-002", "source": "billing-api", "event_type": "request.completed", "occurred_at": "2026-10-21T09:00:04Z", "payload": {"status": 200, "latency_ms": 204}},
    {"event_id": "etl-001", "source": "warehouse-loader", "event_type": "rows.loaded", "occurred_at": "2026-10-21T09:01:00Z", "payload": {"rows": 1840}},
]


class PipelineCheckTests(unittest.TestCase):
    def test_valid_batch_has_no_errors(self):
        result = summarize(SAMPLE)
        self.assertEqual(result["events"], 3)
        self.assertEqual(result["sources"]["billing-api"], 2)
        self.assertEqual(result["errors"], [])

    def test_duplicate_event_is_rejected(self):
        broken = SAMPLE + [dict(SAMPLE[0])]
        self.assertIn("events[3] duplicate event_id api-001", validate_events(broken))

    def test_out_of_order_event_is_rejected(self):
        broken = list(reversed(SAMPLE[:2]))
        self.assertIn("events[1] out of order", validate_events(broken))


if __name__ == "__main__":
    unittest.main()
