return {
    LuaVersion = "LuaU";

    VarNamePrefix = "NETT_WTF_";

    NameGenerator = "MangledShuffled";

    PrettyPrint = false;

    Seed = 0;

    Steps = {
        {
            Name="ProxifyLocals";
        },
        {
            Name="WrapInFunction";
            Settings = {
                Iterations = 2;
            }
        },
        {
            Name="SplitStrings";
            Settings = {
                Treshold = 1;
                ConcatenationType = "strcat";
            }
        },
    }
}