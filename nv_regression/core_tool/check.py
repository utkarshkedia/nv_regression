from pathlib import Path
import sys,os
import scp
a = Path(__file__).resolve().parent.parent
sys.path.append(str(a))
print(os.path.join(a,"abc"))
