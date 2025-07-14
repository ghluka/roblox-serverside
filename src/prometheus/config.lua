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
        },
    }
}