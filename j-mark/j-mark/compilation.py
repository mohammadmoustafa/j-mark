from abc import ABC, abstractmethod
from exceptions import IncompatibleVersionException
import subprocess
import sys
from typing import List

class Compiler(ABC):

  @abstractmethod
  def compile(self):
      pass

class JavaCompiler(Compiler):

  versions = [1.8, 8]

  def __init__(self,
              classpath: str,
              source: float,
              target: float,
              files: List[str],
              junit: bool) -> None:
      self.classpath = classpath
      self.source = source
      self.target = target
      self.files = files
      self.junit = junit
      try:
          self.check_version(self.source)
      except IncompatibleVersionException as e:
          print(f"Source {e}", file=sys.stderr)

      try:
          self.check_version(self.target)
      except IncompatibleVersionException as e:
          print(f"Target {e}", file=sys.stderr)
  
  def check_version(self, version: float) -> IncompatibleVersionException:
      if not (version in self.versions):
        raise IncompatibleVersionException(f'version not supported by j-Mark.'
          + 'Version must be {min(self.versions)} or higher.')

  def compile(self):
    command = [
                "javac", 
                "-source",
                f"{self.source}",
                "-target",
                f"{self.target}", 
                "-cp",
                f"{self.classpath}",
                " ".join(self.files),
              ]
    print(" ".join(command))
    process = subprocess.run(command, capture_output=True)
    if process.returncode != 0:
      print(f"Process exited with return code {process.returncode}", file=sys.stderr)
      output = (process.stderr).decode("utf-8")
      print(f"Output: {output}")
