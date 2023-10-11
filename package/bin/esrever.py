"""" streaming search command that reverses the requestsed """
import json
import os
import sys
from typing import Any, Dict, Generator, List


libpath = os.path.dirname(__file__).replace('/bin', '/lib')
sys.path.append(libpath)


from splunklib.searchcommands import ( #type: ignore # noqa: E402
    Configuration,
    Option,
    StreamingCommand,
    dispatch,
)
# from splunklib.searchcommands.validators import Fieldname #noqa: E402

class StopProcessing(Exception):
    """custom error to yeet us out of the loop"""

@Configuration()
class Reverse(StreamingCommand): # type: ignore
    """
    Reverses the requested field, if it's found.

    """
    field = Option(
        doc="""
        **Syntax:** **field=***<field>*
        **Description:** The field to reverse.""",
        require=False,
        default="en",
        # validate=Fieldname(),
    )

    fields = Option(
        doc="""
        **Syntax:** **field=***<field>*
        **Description:** A comma-delimited set of fields to reverse.""",
        require=False,
        default="",
        # validate=Fieldname(),
    )

    log_level = Option(
        doc="""
        **Syntax:** **field=***<field>*
        **Description:** The log level to set, defaults to INFO.""",
        require=False,
        default="INFO",
        # validate=Fieldname(),
    )

    @property
    def fields_to_process(self) -> List[str]:
        """gets the fields to process"""
        res = []
        if self.field is not None:
            res.append(self.field)
        if self.fields is not None:
            res.extend([field.strip() for field in self.fields.split(",")])
        return res

    @property
    def log_level_prop(self) -> str:
        """gets the language code"""
        if self.log_level is None:
            return "INFO"
        res: str = self.log_level.strip().upper()
        return res

    def stream(self, records: List[Dict[str, Any]]) -> Generator[Any, None, None]:
        """this is the main part of the function, streaming the
            results through the checks"""
        self.logger.debug("reversing the following fields %s", self.fields_to_process)
        for record in records:
            # process the raw data
            if isinstance(record, dict) and "_raw" in record:
                try:
                    data = json.loads(record.get("_raw", "{}"))
                    for field in self.fields_to_process:
                        if field in data:
                            data[field] = data[field][::-1]
                    record["_raw"] = json.dumps(data, default=str, ensure_ascii=False)
                except json.JSONDecodeError as jde:
                    self.logger.error("Failed to decode _raw as JSON: %s input: %s", jde, record)

            for field in self.fields_to_process:
                if field in record:
                    record[field] = record[field][::-1]

            yield record

dispatch(Reverse, sys.argv, sys.stdin, sys.stdout, __name__)
