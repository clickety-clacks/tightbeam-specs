alias Tightbeam.ClientE2E.SimClient

host = "127.0.0.1"
port = 12_374
device_id = "release018-s1b"

case SimClient.pair(host, port,
       device_id: device_id,
       claimed_name: "mike"
     ) do
  {:ok, %{token: token, user_id: user_id}} ->
    IO.puts("PAIR_OK user_id=#{user_id} token=[redacted]")

    case SimClient.connect(host, port, token, device_id: device_id) do
      {:ok, client} ->
        auth = SimClient.find(client, 0, &(&1["type"] == "auth_result"))
        snapshot = SimClient.find(client, 0, &(&1["type"] == "stream_snapshot"))
        sync = SimClient.find(client, 0, &(&1["type"] == "sync_complete"))
        streams = (snapshot && snapshot["streams"]) || []
        main = Enum.find(streams, &(&1["kind"] == "main"))

        evidence = %{
          pair_user_id: user_id,
          connected_user_id: client.user_id,
          connected_is_admin: client.is_admin,
          auth_success: auth && auth["success"],
          auth_user_id: auth && auth["userId"],
          auth_is_admin: auth && auth["isAdmin"],
          sync_complete: not is_nil(sync),
          main: main && Map.take(main, ["sessionKey", "displayName", "kind", "ownerUserId"])
        }

        IO.inspect(evidence, label: "CONNECT_EVIDENCE", pretty: false)
        SimClient.disconnect(client)

        if client.user_id == user_id and client.is_admin and auth["success"] == true and
             not is_nil(main) and not is_nil(sync) do
          IO.puts("S1B_PASS")
        else
          IO.puts(:stderr, "S1B_FAIL incomplete pair/connect evidence")
          System.halt(2)
        end

      {:error, reason} ->
        IO.puts(:stderr, "CONNECT_FAIL #{inspect(reason)}")
        System.halt(3)
    end

  {:error, reason} ->
    IO.puts(:stderr, "PAIR_FAIL #{inspect(reason)}")
    System.halt(4)
end
